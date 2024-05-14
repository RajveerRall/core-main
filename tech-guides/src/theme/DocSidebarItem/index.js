import React from 'react';
import DocSidebarItem from '@theme-original/DocSidebarItem';

// AL custom ==> All code replaced

// AL custom ==> Start (add unlisted feature)
const DocSidebarItemWrapper = (props) => {
	const isUnlisted = (props.item.customProps || {}).unlisted;
	const isCurrentPage =
		props.item.type === "link" && props.item.href === props.activePath;

	if (isUnlisted && !isCurrentPage) {
		return null;
	}

	return <DocSidebarItem {...props} />;
};

export default DocSidebarItemWrapper;
// AL custom ==> End
